Vue.component('model-create', {
  template: '<div>' +
    '<div class="form-group">' +
      '<label>Name</label>' +
      '<input class="form-control" name="name" v-model="model.name"/>' +
    '</div>' +
    '<div class="form-group">' +
      '<button class="btn btn-default" @click="create">Create</button>' +
    '</div>' +
  '</div>',

  data () {
    return {
      model: {}
    }
  },

  methods: {
    create () {
      var config = { headers: { 'Content-Type': 'multipart/form-data' } };
      // var params = {
      //   name: this.model.name
      // };
      var params = new FormData();
      // data.append('action', 'ADD');
      params.append('name', this.model.name);
      axios.post('/models', params, config)
        .then((response) => {
          window.location.reload(true);
        });
    }
  }
});
