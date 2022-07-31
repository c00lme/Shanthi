<script>
  import { fade } from 'svelte/transition';
  import Footer from './Footer.svelte'
  import {push} from "svelte-spa-router"

  const jwt = localStorage.getItem("jwt");
  const user = localStorage.getItem("username");

  window.document.body.classList.remove('gradient')

  if(jwt == null || user == null){
    push("/login")
  }
  
  let promise = Promise.resolve([]);
  let result = null;

	async function recsReq() {

		const response = await self.fetch('https://YouthfulInconsequentialUpgrade-1.hydrabeans.repl.co/get-recs', {
			method: 'POST',
      headers: {
        "Authorization": jwt,
        "content-type": "application/json"
      }
		})

    const json = await response.json()
    
		if (response.ok) {
      return json
    }
    throw new Error(json.error)

	}

  promise = recsReq();
  
  
</script>
  <div class="dailyHeader">
      Good Evening, {user}
  </div>
  {#await promise}
  {:then recs}
    {#each recs as lesson, i}
      <div class="lessonGeneralTime" in:fade>
        
        {#if i == 0}
        	Morning
        {:else if i == 1}
        	Afternoon
        {:else if i == 3}
        	Evening
        {/if}
      </div>
  		<div class="lesson">
        <button class="lessonButton" in:fade>
          <img src={lesson.preview} class="lessonPreview" alt="background image" />
          <div class="lessonTitle">
            {lesson.title}          
          </div>
          <div class="lessonTime">🕑 {lesson.time}</div>
          <div class="lessonType">🎤 {lesson.type}</div>
  		  </button>  
      </div>
    {/each}
  {:catch error}
    {error.message}
  {/await}
  <Footer/>
<style>

  .lessonGeneralTime{
    color: white;
    font-size: 1.3rem;
    font-weight: bold;
    
  }
  .dailyHeader{
    color: white;
    margin-bottom: 0.5em;
    font-size: 1.7rem;
    line-height: 1.7em;
    font-weight: bold;
    padding: 1em;    
    border-radius: 0.75em;


  }
  .lessonButton {
    font-family: inherit;
    font-size: inherit;
    color: white;
    text-align: left;
    padding: 0.7em;
    border-radius: 0.75em;
    border-style: solid;
    width: 19em;
    margin: 0.7em;
    min-height: 4em;
    border-width: 0.15em;
    border-color: hsla(276, 100%, 40%, 1);
    background-color: #23272a;

  }

  .lessonPreview {
    width: 6em;
    object-fit: fill;
    float: right;
    border-radius: 0.75em;
    margin-left: 0.3em;
  }
  .lessonTitle{
    font-weight: bold;
  }

  button:active {
    filter: brightness(85%);
  }
</style>
