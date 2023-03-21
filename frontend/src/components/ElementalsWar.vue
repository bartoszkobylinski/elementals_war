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
          <img :src="element.fields.image" alt="element" />
        </div>
        <button @click="clearPlayerHand">Clear Hand</button>
      </div>
      <div class="player-hand-entities">
        <div class="entity-wrapper" v-for="(entity, index) in groupedEntities" :key="'entity-' + index">
          <entity-card :entity="entity" />
        </div>
      </div>
      <p v-else>No elements in hand.</p>
    </div>
  </div>
</template>

<script>
import ElementCard from "@/components/ElementCard.vue";
import EntityCard from "@/components/EntityCard.vue";



import axios from 'axios';
import {
  clearPlayerHand,
  flipCard,
  updatePlayerHand,
  compareCards,
  getCsrfToken,
  groupedEntities,
  getCookie} from "@/components/ElementalsWarMethods";

const csrfToken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrfToken');
axios.defaults.headers.common['Content-Type'] = 'application/json';

export default {
  components: {
    ElementCard,
    EntityCard,
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
    clearPlayerHand,
    flipCard,
    updatePlayerHand,
    compareCards,
    getCsrfToken,
    },
  computed: {
  groupedEntities,
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
  width: 70%;
  margin: 0 auto;
}

.player-hand-elements {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.player-hand .element-wrapper {
  flex-basis: calc(20% - 10px);
  margin: 5px;
}

.player-hand img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

.player-hand p {
  margin-top: 20px;
}

</style>
