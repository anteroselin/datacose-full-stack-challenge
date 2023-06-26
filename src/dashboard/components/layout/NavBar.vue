<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <nuxt-link class="navbar-brand" to="/">Home</nuxt-link>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <nuxt-link class="nav-link" to="/authors">Authors</nuxt-link>
          </li>
          <li class="nav-item">
            <nuxt-link class="nav-link" to="/books">Books</nuxt-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
