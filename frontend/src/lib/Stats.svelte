<script>
  import { fade } from 'svelte/transition';
  import {push} from "svelte-spa-router"
  import Footer from './Footer.svelte'
  
  const jwt = localStorage.getItem("jwt");
  const user = localStorage.getItem("username");


  window.document.body.classList.remove('gradient')

  if(jwt == null || user == null){
    push("/login")
  }
  else{
    console.log(jwt)
  }
  
  let promise = Promise.resolve([]);
  let result = null;

	async function statsReq() {

		const response = await self.fetch('https://YouthfulInconsequentialUpgrade-1.hydrabeans.repl.co/graph-data', {
			method: 'GET',
      headers: {
        "Authorization": jwt,
      }
		})

    const json = await response.json()
    
		if (response.ok) {
      return json
    }
    throw new Error(json.error)

	}

  promise = statsReq();
  
  //this data will be substituted with the actual data sent from backend
  
  let data = {
    hours: "30",
    favorite: "Mindfulness",
    focus: "Anxiety"
  }
  
</script>

  <div class="statsHeader">
    These are your statistics {user}
  </div>
  <div class="stats" in:fade>
    <div class="timeStats">Time: <span style="color:red">{data.hours} Hours</span></div>
    <div class="favoriteStats">Favorite: <span style="color:yellow">{data.favorite}</span></div>
    <div class="focusStats">Focus: <span style="color:green">{data.focus}</span></div>
  </div>
  {#await promise}
  {:then graph}
  <div class="graph" in:fade>
    <div class="graphTitle">Your Data</div>
    <img src={graph.graph} class="graph" alt="graph"/>
  </div>
  {:catch error}
    {error.message}
  {/await}
  <Footer/>

<style>
  .graph {
    width: 16em;
    display: inline-block;
    vertical-align: middle;
    object-fit: fill;
    border-radius: 0.75em;
    line-height: 2em;
    font-size: 1.3rem;
    font-weight: bold;

  }
  .statsHeader{
    margin-bottom: 0.5em;
    font-size: 1.7rem;
    line-height: 1.7em;
    font-weight: bold;
    padding: 1em;    
    border-radius: 0.75em;
  }
  .stats{
    margin-bottom: 0.5em;
    font-size: 1.3rem;
    line-height: 1.7em;
    font-weight: bold;
    padding: 1em;    
    border-radius: 0.75em;
  }
</style>
