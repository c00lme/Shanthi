<script>
  import Logo from './Logo.svelte'
  import {push} from "svelte-spa-router"
  
  window.document.body.classList.add('gradient')

  
  let username = "";
  let password = "";

  let promise = Promise.resolve([]);

	async function signupReq() {

		const response = await self.fetch('https://YouthfulInconsequentialUpgrade-1.hydrabeans.repl.co/signup', {
			method: 'POST',
			body: JSON.stringify(
				{"username": username,"password": password}
			),
      headers: {
        "content-type": "application/json"
      }
		})
    
		if (response.ok) {
      
      push("/login");
      
    }
    throw new Error("user already exists");
    

	}

  function signup() {
    promise = signupReq();
  }
</script>


<Logo/>
<div class="signup">
  <div class="signupTitle">
    Signup
  </div>
  <input bind:value={username} placeholder="Username" class="signupInput">
  <input bind:value={password} placeholder="Password" class="signupInput">
  <button on:click={signup} class="signupButton">
    {#await promise}
	    Loading...
    {:then result}
      Signup
    {:catch error}
      {error.message}
    {/await}
  </button> 
  already have an account? <a href="#/login" style="color: yellow"to="/signup">Login</a>

</div>

<style>
  .signupTitle {
    font-size: 2rem;
    font-weight: bold;
  }
  .signupInput {
    font-family: inherit;
    font-size: inherit;
    border: none;
    border-radius: 0.75em;
    text-align: center;
    width: 100%;
    height: 3em;

  }
  .signupButton {
    color: white;
    font-family: inherit;
    font-size: inherit;
    padding: 0em;
    width: 100%;
    border: none;
    border-radius: 0.75em;
    height: 3em;
    text-align: center;
    background: linear-gradient(90deg, hsla(276, 100%, 40%, 1) 0%, hsla(264, 68%, 40%, 1) 100%);  
  }

  .signup {
    line-height: 4em;
    font-family: inherit;
    font-size: inherit;
    padding: 2em;
    border: none;
    border-radius: 0.75em;
    width: 70%;
    height: 19em;
    background: transparent;
    position: absolute;
    background-color: #23272a;
    max-width: 25em;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  button:active {
    filter: brightness(85%);
  }
</style>
