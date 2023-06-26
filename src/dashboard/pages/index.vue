<template>
  <div>
    <div v-if="isAuthenticated">
      <h1>Welcome</h1>
      <b-button @click="logout" variant="primary">Logout</b-button>
    </div>
    <div v-else>
      <h3 class="text-center">Sing In</h3>
      <SignInForm class="mt-4" />
    </div>
  </div>
</template>

<script>
import SignInForm from '~/components/login/SignInForm.vue';

export default {
  components: {
    SignInForm,
  },
  computed: {
    isAuthenticated() {
      return this.$accessor.auth.isAuthenticated;
    },
  },
  methods: {
    async logout() {
      await this.$accessor.auth.logout();
    },
  },
};
</script>
