<template>
  <div class="card" :class="size" @click="flip">
    <img :src="element.flipped ? element.fields.image : backImageUrl" alt="element" />
    <div v-if="element.count" class="count">{{ element.count }}</div>
  </div>
</template>

<script>
import config from "../../config";
export default {
  props: ['element','size'],
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
  width: 150px;
  height: 150px;
  cursor: pointer;
}
.card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.card.small {
  width: 50px;
  height: 50px;
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
