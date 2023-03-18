<template>
  <div class="card" @click="flip">
    <img :src="element.flipped ? element.fields.image : backImageUrl" alt="element" />
  </div>
</template>

<script>
import config from "../../config";
export default {
  props: ['element'],
  emits: ['card-click'],
  data() {
    return {
      backImageUrl: config.BACK_IMAGE_URL,
    };
  },
  methods: {
    flip() {
      this.$emit('card-click');
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
