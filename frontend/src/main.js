import { createApp } from 'vue';
import axios from "axios";
import App from "@/App.vue";
import ElementalsWar from "@/components/ElementalsWar.vue";
import ElementCard from "@/components/ElementCard.vue";

const app = createApp(App);

app.component('elementals-war', ElementalsWar)
app.component('element-card', ElementCard)

app.config.globalProperties.$http = axios;

app.mount("#app")
