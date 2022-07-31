<script>
  import Router from "svelte-spa-router";
  import Footer from "./lib/Footer.svelte"
  import Daily from './lib/Daily.svelte'
  import Stats from './lib/Stats.svelte'
  import Login from './lib/Login.svelte'
  import Signup from './lib/Signup.svelte'

  let routes = {
    "/": Daily,
    "/signup": Signup,
    "/login": Login,
    "/stats": Stats
  }

</script>
<main>
  <Router {routes}/>

</main>


<style>
  @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@300;600&display=swap');
  :global(body) {
    font-family: 'Mulish', sans-serif;
    background: #2f3136;
    color: white;
  }
  :global(body.gradient) {
    background: linear-gradient(90deg, hsla(276, 100%, 40%, 1) 0%, hsla(264, 68%, 40%, 1) 100%);
  }

  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
  }

  
</style>
