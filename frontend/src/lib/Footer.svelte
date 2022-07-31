<script>
  import {push} from "svelte-spa-router"
  function goHome(){
    push("/")
  }
  function goStats(){
    push("/stats")
  }
  function logout(){
    localStorage.removeItem("jwt");
    localStorage.removeItem("username");
    push("/login")
  }
</script>

<div class="footerTopMargin"></div>
<div class="footer">

  <button on:click={goHome} class="footerButton">
    <div class="footerIcon">🌅</div>
    Today
  </button>
  <button on:click={goStats} class="footerButton">
    <div class="footerIcon">📈</div>
    Stats
  </button>
  <button on:click={logout} class="footerButton">
    <div class="footerIcon">🚪</div>
    Logout
  </button>
</div>



<style>
  .footerTopMargin{
    margin-top: 4em;
  }
  .footer {
    bottom: 0;
    left: 0; 
    right: 0; 
    position: fixed;
    border-top: solid;
    border-width: 0.15em;
    border-color: hsla(276, 100%, 40%, 1);
    background-color: #23272a;

  }

  .footerButton {
    font-family: inherit;
    font-size: inherit;
    text-align: left;
    background-color: transparent;
    color: white;
    border: none;
    width: 6em;
    min-height: 4em;
    text-align: center;
  }

  .footerIcon{
    font-size: 1.5rem;
  }

  button:active {
    background-color: #2f3136;
  }

</style>
