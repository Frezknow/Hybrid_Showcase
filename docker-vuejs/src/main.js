import { createApp } from 'vue'
import App from './App.vue'
import VueAxios from './plugins/axios'

createApp(VueAxios)
createApp(App).mount('#app')
