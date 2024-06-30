<template>
	<div class="">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs
				class="h-7"
				:items="[{ label: __('EventJobs'), route: { name: 'EventJobs' } }]"
			/>
			<div class="flex">
				<router-link
					v-if="user.data?.name"
					:to="{
						name: 'EventJobCreation',
						params: {
							eventjobName: 'new',
						},
					}"
				>
					<Button variant="solid">
						<template #prefix>
							<Plus class="h-4 w-4" />
						</template>
						{{ __('New EventJob') }}
					</Button>
				</router-link>
			</div>
		</header>
		<div v-if="eventjobs.data?.length">
			<div class="divide-y lg:w-3/4 mx-auto p-5">
				<div v-for="eventjob in eventjobs.data">
					<router-link
						:to="{
							name: 'EventJobDetail',
							params: { eventjob: eventjob.name },
						}"
						:key="eventjob.name"
					>
						<EventJobCard :eventjob="eventjob" />
					</router-link>
				</div>
			</div>
		</div>
		<div v-else class="text-gray-700 italic p-5 w-fit mx-auto">
			{{ __('No eventjobs posted') }}
		</div>
	</div>
</template>
<script setup>
import { Button, Breadcrumbs, createResource } from 'frappe-ui'
import { Plus } from 'lucide-vue-next'
import { inject, computed } from 'vue'
import EventJobCard from '@/components/EventJobCard.vue'
import { updateDocumentTitle } from '@/utils'

const user = inject('$user')

const eventjobs = createResource({
	url: 'eventsconnect.eventsconnect.api.get_eventjob_opportunities',
	cache: ['eventjobs'],
	auto: true,
})

const pageMeta = computed(() => {
	return {
		title: 'EventJobs',
		description: 'An open eventjob board for the community',
	}
})

updateDocumentTitle(pageMeta)
</script>
