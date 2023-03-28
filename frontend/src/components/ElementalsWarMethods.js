import axios from "axios";

const csrfToken=getCookie('csrftoken')
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

async function clearPlayerHand() {
      try {
        console.log("Clearing player hand....", this.player.id)
        const response = await axios.post("http://localhost:8000/api/clear_hand/", {
          player_id: this.player.id,
          },
            {
            withCredentials: true,
          });
        console.log("Response:", response.data)
        if (response.data.status === 'success') {
          this.player.hand = [];
        } else {
          console.error("Error clearing player hand:", response.data.message);
        }
      } catch (error) {
        console.error('Error clearing player hand:', error);
        }
      }

function flipCard(index) {
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
    }

async function updatePlayerHand(element) {
      try {
        const response = await axios.post("http://localhost:8000/api/update_hand/", {
          player_id: this.player.id,
          element_id: element.pk,
            }, {
              withCredentials: true,
            });
        if (response.data.status === 'success') {
          this.player.hand.push(element);
        } else {
          console.error("Error updating player hand:", response.data.message);
          }
      } catch (error) {
        console.error('Error updating player hand:', error);
        }
      }

async function compareCards() {
      if (this.flippedCards[0].fields.element_type === this.flippedCards[1].fields.element_type) {
        this.matchedPairs.push(...this.flippedCards);
        for (const card of this.flippedCards) {
          await this.updatePlayerHand(card);
          }

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
}

function getCsrfToken() {
      return csrfToken;
      }

async function groupedEntities() {
  const grouped = this.player.hand.reduce((acc, element) => {
    acc[element.fields.element_type] = (acc[element.fields.element_type] || 0) + 1;
    return acc;
  }, {});

  const entities = await Promise.all(
    Object.entries(grouped)
      .filter(([, count]) => count >= 3)
      .map(async ([entityType]) => {
          console.log('Fetching entity image URL for:', entityType);
          const imageURL = await fetchEntityImageURL(entityType);
          console.log('Entity image URL:', imageURL);
          return {
            entity_type: entityType,
            image: imageURL,
          };
      })
  );

  return entities;
}

async function exchangeCards() {
    if (this.selectedCards.length !==3){
        alert("Please select exactly 3 cards to exchange.");
        return;
    }
    const elementType = this.selectedCards[0].fields.element_type;
    if (!this.selectedCards.every((card)=> card.fields.element_type === elementType)) {
        alert("Please select 3 cards of the same element type.");
        return;
    }
    this.player.hand = this.player.hand.filter((card) => !this.selectedCards.includes(card));
    const imageURL = await fetchEntityImageURL(elementType);
    this.player.hand.push({fields: {image: imageURL, entity_type: elementType}});
}

async function fetchEntityImageURL(entityType) {
    console.log('groupedEntities called');
  try {
    const response = await axios.get(`http://localhost:8000/api/entity_image/${entityType}/`);
    if (Array.isArray(response.data)) {
      const entity = response.data[0];
      console.log("heeeeej")
      console.log(entity)
      return entity.image_url;
    } else {
      return response.data.image_url;
    }
  } catch (error) {
    console.error('Error fetching entity image URL:', error);
    return null;
  }
}

export {
    getCookie,
    clearPlayerHand,
    flipCard,
    updatePlayerHand,
    compareCards,
    getCsrfToken,
    groupedEntities,
    exchangeCards,
};
