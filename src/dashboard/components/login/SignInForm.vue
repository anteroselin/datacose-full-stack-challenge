<template>
  <div>
    <b-form @submit.prevent="handleSignIn">
      <b-form-group id="username" label="Username:" label-for="input-username" label-cols-lg="2">
        <b-form-input v-model="userInfo.username" required></b-form-input>
      </b-form-group>
      <b-form-group id="password" label="Password:" label-for="input-password" label-cols-lg="2">
        <b-form-input type="password" v-model="userInfo.password" required></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary" class="float-right">Sign In</b-button>
    </b-form>
  </div>
</template>

<script lang="ts">
export default {
  data() {
    return {
      userInfo: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    async handleSignIn() {
      const formData = new FormData();
      for (let [key, value] of Object.entries(this.userInfo)) {
        formData.append(key, value);
      }
      await this.$accessor.auth.login({ formData });
    },
  },
};
</script>
