<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import Logo from './Logo.svelte'
  import {push} from "svelte-spa-router"

  
  window.document.body.classList.add('gradient')

  let username = "";
  let password = "";
  let result = null;

  let promise = Promise.resolve([]);

	async function loginReq() {

		const response = await self.fetch('https://YouthfulInconsequentialUpgrade-1.hydrabeans.repl.co/signin', {
			method: 'POST',
			body: JSON.stringify(
				{"username": username,"password": password}
			),
      headers: {
        "content-type": "application/json"
      }
		})

    const json = await response.json()
    
		if (response.ok) {
      localStorage.setItem("jwt", json.jwt);
      localStorage.setItem("username", username);
      push("/");

    }
    throw new Error(json.error)

	}

  function login() {
    promise = loginReq();
  }

</script>


<Logo/>
<div class="login">
  <div class="loginTitle">
    Login
  </div>
  <input bind:value={username} placeholder="Username" class="loginInput">
  <input bind:value={password} placeholder="Password" class="loginInput">
  <button on:click={login} class="loginButton">
    {#await promise}
	    Loading...
    {:then result}
      Login
    {:catch error}
      {error.message}
    {/await}
  </button>
  don't have an account? <a href="#/signup" style="color: yellow"to="/signup">Register</a>

</div>

<style>
  
  .loginTitle {
    font-size: 2rem;
    font-weight: bold;
  }
  .loginInput {
    font-family: inherit;
    font-size: inherit;
    border: none;
    border-radius: 0.75em;
    text-align: center;
    width: 100%;
    height: 3em;

  }
  .loginButton {
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
  .login {
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
