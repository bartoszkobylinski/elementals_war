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
import ElementCard from "@/components/ElementCard.vue";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

import axios from 'axios';

const csrfToken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrfToken');
axios.defaults.headers.common['Content-Type'] = 'application/json';

export default {
  components: {
    ElementCard,
  },
  data() {
    console.log("ElementalsWar data function called")
    return {
      elements: [],
      player: {
        id: null,
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
    async updatePlayerHand(elementId) {
      try {
        const response = await axios.post("http://localhost:8000/api/update_hand/", {
          player_id: this.player.id,
          element_id: elementId,
            }, {
          withCredentials: true,
            });
        if (response.data.status === 'success') {
          this.player.hand.push(elementId);
        } else {
          console.error("Error updating player hand:", response.data.message);
        }
      } catch (error) {
        console.error('Error updating player hand:', error);
        }
    },
    async compareCards() {
      if (this.flippedCards[0].fields.element_type === this.flippedCards[1].fields.element_type) {
        this.matchedPairs.push(...this.flippedCards);
        const newElementId = this.flippedCards[0].pk;
        await this.updatePlayerHand(newElementId);

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
    getCsrfToken() {
      return csrfToken;
    },
  },
  async created() {
      console.log("mounted() method called")
      try {
        const response = await axios.get('http://localhost:8000/api/board/');
        this.elements = response.data.board.flat();
        this.player.id = response.data.player.pk;
        this.player.name = response.data.player.fields.name;
        this.player.hand = response.data.player.fields.hand;
        console.log(response.data)
      } catch (error) {
        console.error('Error fetching element data:', error);
      }
    },
}
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
