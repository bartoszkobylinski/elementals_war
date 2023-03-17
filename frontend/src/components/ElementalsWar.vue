<template>
  <div>
    <div class="board">
      <div class="element-wrapper" v-for="(element, index) in elements" :key="index">
        <element-card :element="element" @card-click="flipCard(index)" />
      </div>
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
      this.elements = response.data.board.flat();
      console.log(response.data.board)
    } catch (error) {
      console.error('Error fetching element data:', error);
    }
  },
};
</script>

<style scoped>
.board {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.element-wrapper {
  flex-basis: calc(33.333% - 10px);
  margin-bottom: 10px;
}
</style>