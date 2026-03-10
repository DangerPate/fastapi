import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/global.css'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

createApp(App).mount('#app')
const app = createApp(App)
app.use(router)
app.mount('#app')
app.use(Toast, {
  position: 'bottom-right',     
  timeout: 4000,                
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,       
  closeButton: 'button',
  icon: false,                   
  rtl: false,
  transition: 'Vue-Toastification__bounce',
  maxToasts: 5,
  newestOnTop: true
})