<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const activeItem = ref('Products') // consider activating Products by default
</script>

<template>
	<header>
		<nav class="navbar navbar-expand-lg bg-body-tertiary navmain">
			<div class="container-fluid">
				<a class="navbar-brand navbar-brand-custom">BankGPT</a>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse" id="navbarNav">
					<ul class="navbar-nav">
						<li class="nav-item" :class="{ 'active-nav-item': activeItem === 'Products' }" @click="activeItem = 'Products'">
							<RouterLink class="nav-link" to="/">Products</RouterLink>
						</li>
						<li class="nav-item" :class="{ 'active-nav-item': activeItem === 'My Account' }" @click="activeItem = 'My Account'">
							<RouterLink class="nav-link" to="/my-account">My Account</RouterLink>
						</li>
					</ul>
				</div>
			</div>
		</nav>
	</header>

	<RouterView />
</template>

<style>
	.navbar-brand-custom {
		margin-left: 30px;
		font-size: 55px;
		font-family: 'Consolas', serif;
		font-weight: bold;
	}
	.navmain {
  		background-color: rgb(255, 159, 70);
	}
	.nav-item {
		margin-left: 20px;
		background-color: antiquewhite;
		border: none;
		border-radius: 4px;
		font-size: 24px;
		font-weight: bold;
    	font-family: Arial, sans-serif;
		color: black;
	}

	.active-nav-item {
		background-color: #f0ec0e; /* color after clicking */
		border: 2px solid black; /* add black edge */
	}

	@keyframes movingBackground {
		0% { background-position: 0% 50%; }
		50% { background-position: 100% 50%; }
		100% { background-position: 0% 50%; }
	}

	body {
		background: linear-gradient(-45deg, #b9e1fd, #fdf7c3, #8ed8fa, #e7aef1);
		background-size: 400% 400%;
		animation: movingBackground 30s ease infinite;
	}
</style>
