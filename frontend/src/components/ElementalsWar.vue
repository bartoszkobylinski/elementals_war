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
import axios from 'axios';
import ElementCard from './ElementCard.vue';

export default {
  components: {
    ElementCard,
  },
  data() {
    return {
      elements: [],
    };
  },
  methods: {
    flipCard(index) {
      this.elements[index].flipped = !this.elements[index].flipped;
    },
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:8000/api/board/');
      this.elements = response.data;
    } catch (error) {
      console.error('Error fetching element data:', error);
    }
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

