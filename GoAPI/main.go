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
	"time"
)

const MAX_UPLOAD_SIZE = 1024 * 1024 * 10 // 1MB
var db *sql.DB

type Prediction struct {
	ID         string `json:"id"`
	Prediction string `json:"prediction"`
	//more to come below this
}

//Image      string `json:"image"`
func handleRequests() {
	apiRouter := mux.NewRouter().StrictSlash(true)
	apiRouter.HandleFunc("/all", all).Methods("GET", "OPTIONS")
	apiRouter.HandleFunc("/predict", predict).Methods("POST", "OPTIONS")
	log.Fatal(http.ListenAndServe(":8081", apiRouter))
}

func main() {
	handleRequests()
}

func all(w http.ResponseWriter, r *http.Request) {
	//Allow CORS here By * or specific origin
	w.Header().Set("Access-Control-Allow-Origin", "*")
	db, err := sql.Open("mysql", "root:test@tcp(172.24.0.2)/dev")
	if err != nil {
		panic(err)
	}
	defer db.Close()
	rows, err := db.Query("SELECT id,prediction FROM predictions")
	if err != nil {
		fmt.Println(err)                              // Ugly debug output
		w.WriteHeader(http.StatusInternalServerError) // Proper HTTP response
		return
	}
	defer rows.Close()
	// An album slice to hold data from returned rows.
	var predictions []Prediction

	// Loop through rows, using Scan to assign column data to struct fields.
	for rows.Next() {
		var pre Prediction
		if err := rows.Scan(&pre.ID, &pre.Prediction); err != nil {
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
	dst, err := os.Create(fmt.Sprintf("./uploads/%d%s", time.Now().UnixNano(), filepath.Ext(fileHeader.Filename)))
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
	db, err := sql.Open("mysql", "root:test@tcp(172.24.0.2)/dev")

	if err != nil {
		panic(err)
	}
	defer db.Close()
	p := "dog"
	stmt, err := db.Prepare("INSERT predictions SET prediction=?")
	if err != nil {
		fmt.Println(err)                              // Ugly debug output
		w.WriteHeader(http.StatusInternalServerError) // Proper HTTP response
		return
	}
	defer stmt.Close()

	res, err := stmt.Exec(p)
	if err != nil {
		fmt.Println(err)                              // Ugly debug output
		w.WriteHeader(http.StatusInternalServerError) // Proper HTTP response
		return
	}
	if res != nil {

	}
	//json.NewEncoder(w).Encode(Predictions)
}
