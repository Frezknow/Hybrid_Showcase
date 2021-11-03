<template>
    <div class="hello">
        <h1>{{ msg }}</h1>
        <a href="https://github.com/Frezknow/Hybrid_Showcase">Hybrid Project's GitHub Repo</a>
        <a href="https://www.sanleeunited.com">Another project | Online Community Platform</a>
        <div style="position:absolute; width:40%; top:300px; height:70%; overflow-y:scroll; right:2%;">
            <h2>Upload image and get live predictions on your photo</h2>
            <input type="file" id="file" class="form-control" ref="myFiles" @change="previewFiles" />
            <button class="form-control btn btn-primary" @click="predict()">Predict</button>
            <h2>Below you will find the previously submitted prediction request and results</h2><hr />
            <div v-for="(p,i) in predictions" :key="i" >Prediction #{{p.id}} made by model(Food Classifer): {{p.prediction}} <br /><img style="width:150px; height:100px;" :src="'http://127.0.0.1:5052/'+p.Img" /></div>
        </div>
        <p style="text-align:center; position:relative; font-size:16pt; width:50%;left:10px; height:auto; float:center; margin-bottom:100px;">
            <img style="width:100%; height:800px;  position:relative;" alt="Hybrid project's diagram" src="../assets/0002.jpg">
            The H.P.P as you can see above in the diagram, is a Hybrid dockerized microservice project that is hosted in AWS (ECS).
            It contains Vue, HTML, CSS, Shell, GoLang, Python + Tensorflow,and  Mysql.
            This project gives the user the ability to predict images by using Python Tensorflow CNN model(s).
            As of right now there is only one transfer model for the user to use that is a food classifier,
            however more models will follow as my experience level grows with Tensorflow and AI.
            All previous submitted images and the predictions the AI model(s) returned will display.
        </p>
    </div>
</template>

<script>
    import { axios } from '@/plugins/axios'
    export default {

        name: 'HelloWorld',
        props: {
            msg: String
        },
        data() {
            return {
                predictions: [],
                files: [],
                go: false,
                aiPre:""
            }
        },
        created() {
            var vm = this
            axios.get("http://hybrid-portfolio-project.us-east-1.elasticbeanstalk.com:82/all")
                .then(r => {
                    console.log(r.data)
                    vm.predictions = r.data
                })
                .catch(f => {
                    alert(f)
                });
        },
        methods: {
            previewFiles() {
                this.files = this.$refs.myFiles.files
            },
            predict() {
                var vm = this
                let formData = new FormData();
                var imgs = this.files;
                console.log(imgs)
                if (imgs[0]) {
                    formData.append('img', imgs[0]);
                    if (parseInt(imgs[0].size) > 10000000) {
                        alert("File is to large, please change size of file.")
                        // this.editBusiness.errors.push("Image is to large, must be less than 10 MBs.")
                    }
                }
                axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
                axios.post("http://hybrid-portfolio-project.us-east-1.elasticbeanstalk.com:5052/predict", formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                   })
                    .then(r => {
                        console.log(r.data)
                        vm.predictions.unshift(r.data)
                        //if (!Array.isArray(vm.predictions) || !vm.predictions.length) vm.predictions = [r.data]
                        //this.goStore()
                    })
                    .catch(f => {
                        console.log(f)      
                    });
            },
         
        }

    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
