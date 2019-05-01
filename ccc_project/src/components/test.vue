<template>

<div>
      <p>{{ status }}</p>

</div>

</template>

<script>

export default {

  data() {
    return {
      status: ''
    }
  },
  created() {
    this.load();

  },
  methods: {
  load() {

  this.$http.get('http://ron-swanson-quotes.herokuapp.com/v2/quotes')
      .then((response) => {
        this.status = response.data[0];

      })
      .catch(function(error) {
        console.log(error);
      })
      }
  }
};

</script>

<style scoped>

</style>
