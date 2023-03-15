<template>
  <div class="card" @click="$emit('click')">
    <img :src="element.flipped ? element.image : 'back.png'" alt="element" />
  </div>
</template>

<script>
export default {
  props: {
    element: {
      type: Object,
      required: true,
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
