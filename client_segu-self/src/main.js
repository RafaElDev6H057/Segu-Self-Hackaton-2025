import './assets/main.css'

import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        Options:{
            darkModeSelector:".my-app-dark"
        },
    }
});
app.use(router)

app.mount('#app')
