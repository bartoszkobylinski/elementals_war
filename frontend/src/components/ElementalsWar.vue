<template>
  <div>
    <div class="board">
      <div class="element-wrapper" v-for="(element, index) in elements" :key="index">
        <element-card :element="element" @card-click="flipCard(index, computerMove)" />
      </div>
    </div>
    <div class="player-hand">
      <h3>{{ player.name }}</h3>
      <div class="player-hand-elements" v-if="player.hand.length > 0">
        <div class="element-wrapper" v-for="(element, index) in player.hand" :key="index">
          <element-card :element="element" size="small" />
          <img :src="element.fields.image" alt="element" />
          <input type="checkbox" :value="index" v-model="selectedCards" :id="`element-${index}`">
          <label :for="`element-${index}`"></label>
        </div>
        <button @click="clearPlayerHand">Clear Hand</button>
      </div>
      <p v-else>No elements in hand.</p>
      <div class="player-hand-entities">
        <div class="entity-wrapper" v-for="(entity, index) in groupedEntities" :key="'entity-' + index">
          <entity-card :entity_type="entity.entity_type" :image="entity.image" />
        </div>
        <button @click="exchangeCards">Exchange Cards</button>
      </div>
    </div>
    <div class="computer-hand">
      <h3> {{ computer.name }}</h3>
      <div class="computer-hand-elements" v-if="computer.hand.length > 0">
        <div class="element-wrapper" v-for="(element, index) in computer.hand" :key="'computer-' + index">
          <element-card :element="element" size="small" />
          <img :src="element.fields.image" alt="element" />
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
  exchangeCards, computerMove,
} from "@/components/ElementalsWarMethods";

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
      computer: {
        id: null,
        name: '',
        hand: [],
      },
      flippedCards: [],
      matchedPairs: [],
      selectedCards: [],
      canFlip: true,
      playerTurn: true,
    };
  },
  methods: {
    computerMove,
    clearPlayerHand,
    flipCard,
    updatePlayerHand,
    compareCards,
    getCsrfToken,
    exchangeCards,
    },
  computed: {
  groupedEntities() {
    console.log('groupedEntities computed property called')
    return groupedEntities.call(this);
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
        if (response.data.computer) {
          this.computer.id = response.data.computer.pk;
          this.computer.name = response.data.computer.fields.name;
          this.computer.hand = response.data.computer.fields.hand;
        }
      } catch (error) {
        console.error('Error fetching element data:', error);
      }

    },
  }
</script>

<style lang="css">
  @import "./elementalsWar.css";
</style>
