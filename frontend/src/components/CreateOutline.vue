<template>
	<div v-if="event">
		<div class="text-xl font-semibold">
			{{ event.title }}
		</div>
		<div v-if="event.chapters.length">
			{{ event.chapters }}
		</div>
		<div v-else class="border bg-white rounded-md p-5 text-center mt-4">
			<div>
				{{
					__(
						'There are no chapters in this event. Create and manage chapters from here.'
					)
				}}
			</div>
			<Button class="mt-4">
				{{ __('Add Chapter') }}
			</Button>
		</div>
	</div>
</template>
<script setup>
const props = defineProps({
	event: {
		type: Object,
		default: {},
	},
})
</script>
