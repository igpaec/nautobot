<template>
  <div class="submit-form">
    <div v-if="!submitted">
      <div class="form-group">
        <label for="title">Title</label>
        <input
          type="text"
          class="form-control"
          id="title"
          required
          v-model="location.title"
          name="title"
        />
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <input
          class="form-control"
          id="description"
          required
          v-model="location.description"
          name="description"
        />
      </div>

      <button @click="saveLocation" class="btn btn-success">Submit</button>
    </div>

    <div v-else>
      <h4>You submitted successfully!</h4>
      <button class="btn btn-success" @click="newLocation">Add</button>
    </div>
  </div>
</template>

<script>
import LocationDataService from "../services/LocationDataService";

export default {
  name: "add-location",
  data() {
    return {
      location: {
        id: null,
        title: "",
        description: "",
        published: false
      },
      submitted: false
    };
  },
  methods: {
    saveLocation() {
      var data = {
        title: this.location.title,
        description: this.location.description
      };

      LocationDataService.create(data)
        .then(response => {
          this.location.id = response.data.id;
          console.log(response.data);
          this.submitted = true;
        })
        .catch(e => {
          console.log(e);
        });
    },
    
    newLocation() {
      this.submitted = false;
      this.location = {};
    }
  }
};
</script>

<style>
.submit-form {
  max-width: 300px;
  margin: auto;
}
</style>
