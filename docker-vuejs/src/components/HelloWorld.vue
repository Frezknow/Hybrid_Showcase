<template>
    <div class="hello">
        <h1>{{ msg }}</h1>
        <a href="https://github.com/Frezknow/Hybrid_Showcase">Hybrid Project's GitHub Repo</a>
        <p style="text-align:center; position:absolute; left:20%; font-size:16pt; width:60%; height:auto; margin-bottom:100px;">
            This project gives the user the ability to predict images by using Python Tensorflow CNN models,
            I have built a few CNN models for the user to choose from. We also display previous submitted images and their predictions theAI  models gave them.
        </p>
        <br/><br/>
        <div style="position:relative; margin-top:100px;">
            <h2>Upload image and get live predictions on your photo</h2>
            <input type="file" id="file" ref="myFiles" @change="previewFiles" /><button @click="predict()">Predict</button>
            <h2>Below you will find the previously submitted prediction request and results</h2><hr />
            <div v-bind:key="i" v-for="(p,i) in predictions">Prediction #{{p.id}} made by model({{p.id}}): {{p.prediction}} <br /><img style="width:150px; height:100px;" :src="p.Img" /></div>
        </div>
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
      }
        },
        created() {
            var vm = this
            axios.get("http://127.0.0.1:8081/all")
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
                axios.post("http://127.0.0.1:8081/predict", formData,{
                     headers: {
                         'Content-Type': 'multipart/form-data'
                     }
                    })
                    .then(r => {
                        console.log(r.data)
                        vm.predictions.push(r.data)
                    })
                    .catch(f => {
                        console.log(f)
                    });
            }
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
