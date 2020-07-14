<template>
  <div class="d-flex flex-wrap">
    <ul v-for="(details, index) in flights" :key=index
      class="col-md-3"
    >
      <flight-details
        :flight="details"
      />
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import FlightDetails from '@/components/FlightDetails.vue'

export default {
  name: 'flights',
  components: {
    FlightDetails
  },
  data () {
    return {
      flights: [],
    }
  },
  methods: {
    getAvailableFlights () {
      const path = 'http://127.0.0.1:5000/all_flights'
      axios.get(path)
        .then((res) => {
          this.flights = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  created () {
    setInterval(() => {
      this.getAvailableFlights()    
    }, 10 * 1000)
  },
  mounted () {
    this.getAvailableFlights()
  }
}
</script>

<style scoped>

</style>
