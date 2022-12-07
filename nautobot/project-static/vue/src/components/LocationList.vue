<template>
  <div class="list row">
    <div class="col-12">
      <h4>Locations List</h4>
      <ul class="list-group">
        <li class="list-group-item"
            :class="{ active: location === currentLocation }"
            v-for="location in locations"
            :key="location.id"
            @click="setActiveLocation(location)"
        >
          <div>{{ location.display }}</div>

        </li>
      </ul>

    </div>
    <div class="col-12">
      <div v-if="currentLocation">
        <h4>Location</h4>
        <div>{{ currentLocation.id }}</div>
        <div>{{ currentLocation.slug }}</div>
        <div>{{ currentLocation.name }}</div>
<!--        <router-link :to="'/locations/' + currentLocation.id" class="badge badge-warning">Edit</router-link>-->
      </div>
      <div v-else>
        <br />
        <p>Please click on a Location...</p>
      </div>
    </div>
  </div>
</template>

<script>
import LocationDataService from "../services/LocationDataService";

export default {
  name: "locations-list",
  data() {
    return {
      locations: [],
      currentLocation: null,
      currentIndex: -1,
      title: ""
    };
  },
  methods: {
    retrieveLocations() {
      LocationDataService.getAll()
        .then(response => {
          this.locations = response.data.results;
          console.log(response.data.results);
        })
        .catch(e => {
          console.log(e);
        });
    },

    refreshList() {
      this.retrieveLocations();
      this.currentLocation = null;
      this.currentIndex = -1;
    },

    setActiveLocation(location) {
      this.currentLocation = location;
      console.log(location.name);
      // this.currentIndex = location ? index : -1;
    },

  },
  mounted() {
    this.retrieveLocations();
  }
};
</script>

<style>
.list {
  text-align: left;
  max-width: 750px;
  margin: auto;
}
</style>
