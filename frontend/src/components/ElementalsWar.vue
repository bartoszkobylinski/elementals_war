<template>
  <div>
    <div class="board">
      <div class="element-wrapper" v-for="(element, index) in elements" :key="index">
        <element-card :element="element" @card-click="flipCard(index)" />
      </div>
    </div>
    <div class="player-hand">
      <h3>{{ player.name }}</h3>
      <div class="player-hand-elements" v-if="player.hand.length > 0">
        <div class="element-wrapper" v-for="(element, index) in player.hand" :key="index">
          <element-card :element="element" />
        </div>
      </div>
      <p v-else>No elements in hand.</p>
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
      player: {
        name: '',
        hand: [],
      },
      flippedCards: [],
      matchedPairs: [],
    };
  },
  methods: {
    flipCard(index) {
      const card = this.elements[index];

      if (card.flipped || this.flippedCards.includes(card) || this.flippedCards.length === 2) {
        return;
      }

      card.flipped = true;
      this.flippedCards.push(card);

      if (this.flippedCards.length === 2) {
        setTimeout(() => {
          this.compareCards();
        }, 1000);
      }
    },
    async compareCards() {
      if (this.flippedCards[0].fields.element_type === this.flippedCards[1].fields.element_type) {
        this.matchedPairs.push(...this.flippedCards);
        // Fetch a new board from the backend
        try {
          const response = await this.$http.get('http://localhost:8000/api/board/');
          this.elements = response.data.board.flat();
        } catch (error) {
          console.error('Error fetching new board data:', error);
        }
      }
      this.flippedCards.forEach((card) => {
        card.flipped = false;
      });
      this.flippedCards = [];
    },
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:8000/api/board/');
      this.elements = response.data.board.flat();
      this.player.name = response.data.player.fields.name;
      this.player.hand = response.data.player.fields.hand;
      console.log(response.data)
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
  justify-content: center;
  width: 70%;
  margin: 0 auto;
  border: 1px solid black;
  padding: 10px;
  box-sizing: border-box;
}
.element-wrapper {
  flex-basis: calc(33.333% - 10px);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.player-hand {
  margin-top: 20px;
  text-align: center;
}

.player-hand-elements {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid black;
  padding: 10px;
  margin: 0 auto;
  width: 70%;
}

.element-wrapper {
  flex-basis: calc(33.333% - 10px);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}
</style>
