<template>
  <div v-if="currentLocation" class="edit-form">
    <h4>Location</h4>

    <button type="submit" class="badge badge-success"
      @click="updateLocation"
    >
      Update
    </button>
    <p>{{ message }}</p>
  </div>

  <div v-else>
    <br />
    <p>Please click on a Location...</p>
  </div>
</template>

<script>
import LocationDataService from "../services/LocationDataService";

export default {
  name: "location-detail",
  data() {
    return {
      currentLocation: null,
      message: ''
    };
  },
  methods: {
    getLocation(id) {
      LocationDataService.get(id)
        .then(response => {
          this.currentLocation = response.data;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
    },

    updateLocation() {
      LocationDataService.update(this.currentLocation.id, this.currentLocation)
        .then(response => {
          console.log(response.data);
          this.message = 'The location was updated successfully!';
        })
        .catch(e => {
          console.log(e);
        });
    },

    deleteLocation() {
      LocationDataService.delete(this.currentLocation.id)
        .then(response => {
          console.log(response.data);
          this.$router.push({ name: "locations" });
        })
        .catch(e => {
          console.log(e);
        });
    }
  },
  mounted() {
    this.message = '';
    this.getLocation(this.$route.params.id);
  }
};
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>
