<template>
  <div class="entity-card" @click="handleClick">
    <img :src="image" alt="entity"/>
  </div>
</template>

<script>
export default {
  props: ["entity_type", "image"],
  methods: {
    handleClick() {
      this.$emit("entity-click",this.entity_type)
    },
  },
};
</script>

<style scoped>
.entity-card {
  width: 100px;
  height: 100px;
}

.entity-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
