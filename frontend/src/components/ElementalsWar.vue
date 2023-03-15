<template>
  <div>
    <div class="board">
      <element-card
        v-for="(element, index) in elements"
        :key="index"
        :element="element"
        @click="flipCard(index)"
      />
    </div>
  </div>
</template>

<script>
import ElementCard from './ElementCard.vue';

export default {
  components: {
    ElementCard,
  },
  data() {
    return {
      elements: [
        // Replace these placeholders with your element data
        { id: 1, name: 'air', image: 'air.png', flipped: false },
        { id: 2, name: 'fire', image: 'fire.png', flipped: false },
        { id: 3, name: 'water', image: 'water.png', flipped: false },
        // Add more elements as needed
      ],
    };
  },
  methods: {
    flipCard(index) {
      this.elements[index].flipped = !this.elements[index].flipped;
    },
  },
};
</script>

<style scoped>
.board {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}
</style>
