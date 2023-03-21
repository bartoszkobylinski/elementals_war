<template>
  <div class="entity-card">
    <img :src="entity.fields.image" alt="entity" />
  </div>
</template>

<script>
export default {
  props: ["entity"],
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
