<template>
  <div class="card" @click="$emit('click')">
    <img :src="element.flipped ? element.image : backImageUrl" alt="element" />
  </div>
</template>

<script>
import config from "../../config";
export default {
  props: ['element'],
  data() {
    return {
      flipped: false,
      backImageUrl: config.BACK_IMAGE_URL,
    };
  },
  methods: {
    flip() {
      this.flipped = !this.flipped;
    },
  },
};
</script>

<style scoped>
.card {
  width: 100px;
  height: 100px;
  cursor: pointer;
}
.card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
