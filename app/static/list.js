Vue.component('model-item', {
  template: '<tr><td>{{ model.id }}</td><td>{{ model.name }}</td></tr>',
  props: {
    model: Object
  }
});

Vue.component('model-list', {
  template: '<table class="table">' +
    '<thead><tr><th>id</th><th>name</th></tr></thead>' +
    '<tbody>' +
      '<model-item v-for="m in models" :key="m.id" :model="m" />' +
    '</tbody>' +
    '</table>',

  data () {
    return {
      models: []
    };
  },

  mounted () {
    this.load();
  },

  methods: {
    load () {
      axios.get('/models')
        .then((response) => {
          this.models = response.data;
        });
    },
  }
});


var app = new Vue({ el: '#list' });
