<template>
  <div class="card" @click="flip">
    <img :src="element.flipped ? element.fields.image : backImageUrl" alt="element" />
    <div v-if="element.count" class="count">{{ element.count }}</div>
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
.count {
  position: absolute;
  bottom: 5px;
  right: 5px;
  font-size: 18px;
  font-weight: bold;
  color: white;
  text-shadow: 1px 1px 1px black;
}
</style>
