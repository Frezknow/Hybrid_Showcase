package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"time"
)

const MAX_UPLOAD_SIZE = 1024 * 1024 * 10

var db *sql.DB

type Prediction struct {
	ID         string `json:"id"`
	Prediction string `json:"prediction"`
	Img        string `json: "img"`
}

func handleRequests() {
	apiRouter := mux.NewRouter().StrictSlash(true)
	apiRouter.HandleFunc("/all", all).Methods("GET", "OPTIONS")
	apiRouter.HandleFunc("/predict", predict).Methods("POST", "OPTIONS")
	apiRouter.PathPrefix("/").Handler(http.FileServer(http.Dir("./uploads/")))
	log.Fatal(http.ListenAndServe(":8081", apiRouter))
}

func main() {

	handleRequests()
}

func all(w http.ResponseWriter, r *http.Request) {
	//Allow CORS here By * or specific origin
	w.Header().Set("Access-Control-Allow-Origin", "*")
	db, err := sql.Open("mysql", "root:test@tcp(172.25.0.2)/dev")
	if err != nil {
		panic(err)
	}
	defer db.Close()
	rows, err := db.Query("SELECT id,prediction,img FROM predictions")
	if err != nil {
		fmt.Println(err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	defer rows.Close()
	var predictions []Prediction
	for rows.Next() {
		var pre Prediction
		if err := rows.Scan(&pre.ID, &pre.Prediction, &pre.Img); err != nil {
			json.NewEncoder(w).Encode(err)
		}
		predictions = append(predictions, pre)
	}
	if err = rows.Err(); err != nil {
		json.NewEncoder(w).Encode(err)
	}

	json.NewEncoder(w).Encode(predictions)
}
func predict(w http.ResponseWriter, r *http.Request) {
	//Allow CORS here By * or specific origin
	w.Header().Set("Access-Control-Allow-Origin", "*")

	r.Body = http.MaxBytesReader(w, r.Body, MAX_UPLOAD_SIZE)
	if err := r.ParseMultipartForm(MAX_UPLOAD_SIZE); err != nil {
		http.Error(w, "The uploaded file is too big. Please choose an file that's less than 10MB in size", http.StatusBadRequest)
		return
	}

	file, fileHeader, err := r.FormFile("img")
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	defer file.Close()
	// Create the uploads folder if it doesn't already exist
	err = os.MkdirAll("./uploads", os.ModePerm)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Create a new file in the uploads directory
	name := time.Now().UnixNano()
	ext := filepath.Ext(fileHeader.Filename)
	storeName := strconv.FormatInt(name, 10) + ext
	dst, err := os.Create(fmt.Sprintf("./uploads/%d%s", name, filepath.Ext(fileHeader.Filename)))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer dst.Close()
	//Copy the uploaded file to the filesystem
	_, err = io.Copy(dst, file)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	//Begin SQL Connection
	db, err := sql.Open("mysql", "root:test@tcp(172.25.0.2)/dev")

	if err != nil {
		panic(err)
	}
	defer db.Close()
	p := "cat"
	stmt, err := db.Prepare("INSERT INTO predictions(prediction,img) VALUES (?,?)")
	if err != nil {
		fmt.Println(err)                              // Ugly debug output
		w.WriteHeader(http.StatusInternalServerError) // Proper HTTP response
		return
	}
	defer stmt.Close()
	res, err := stmt.Exec(p, storeName)
	if err != nil {
		fmt.Println(err)                              // Ugly debug output
		w.WriteHeader(http.StatusInternalServerError) // Proper HTTP response
		return
	}
	fmt.Println(res)
	row, err := db.Query("SELECT id,prediction,img FROM predictions order by id desc limit 1 ")
	if err != nil {
		fmt.Println(err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	defer row.Close()
	var pre Prediction
	for row.Next() {
		if err := row.Scan(&pre.ID, &pre.Prediction, &pre.Img); err != nil {
			json.NewEncoder(w).Encode(err)
		}
	}
	if err = row.Err(); err != nil {
		json.NewEncoder(w).Encode(err)
	}
	fmt.Println(pre)
	json.NewEncoder(w).Encode(pre)
}
