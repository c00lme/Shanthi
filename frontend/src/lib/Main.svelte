<script>
  import { fade } from 'svelte/transition';
  import Logo from './Logo.svelte'

</script>


<Logo/>
<div class="signup">
  <div class="signupTitle">
    Signup
  </div>
  <input placeholder="Email" class="mainButton">
  <input placeholder="Password" class="mainButton">
  <input placeholder="Confirm Password" class="mainButton">
  <button class="signupButton">
    Signup
  </button>  
</div>

<style>
  
  .signupTitle {
    font-size: 2rem;
    font-weight: bold;
  }
  .mainButton {
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
  .main {
    line-height: 4em;
    font-family: inherit;
    font-size: inherit;
    padding: 2em;
    border: none;
    border-radius: 0.75em;
    width: 70%;
    height: 20em;
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
