<template>
  <div class="home">
    <h1>航班动态</h1>
    <flights/>
  </div>
</template>

<script>
// @ is an alias to /src
import Flights from '@/components/Flights.vue'

export default {
  name: 'Home',
  components: {
    Flights
  }
}
</script>
