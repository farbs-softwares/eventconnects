<template>
	<div class="">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs
				class="h-7"
				:items="[
					{
						label: __('EventJobs'),
						route: { name: 'EventJobs' },
					},
					{
						label: eventjob.data?.eventjob_title,
						route: { name: 'EventJobDetail', params: { eventjob: eventjob.data?.name } },
					},
				]"
			/>
			<div v-if="user.data?.name" class="flex">
				<router-link
					v-if="user.data.name == eventjob.data?.owner"
					:to="{
						name: 'EventJobCreation',
						params: { eventjobName: eventjob.data?.name },
					}"
				>
					<Button class="mr-2">
						<template #prefix>
							<Pencil class="h-4 w-4 stroke-1.5" />
						</template>
						{{ __('Edit') }}
					</Button>
				</router-link>
				<Button
					v-if="!eventjobApplication.data?.length"
					variant="solid"
					@click="openApplicationModal()"
				>
					<template #prefix>
						<SendHorizonal class="h-4 w-4" />
					</template>
					{{ __('Apply') }}
				</Button>
			</div>
			<div v-else>
				<Button @click="redirectToLogin(eventjob.data?.name)">
					<span>
						{{ __('Login to apply') }}
					</span>
				</Button>
			</div>
		</header>
		<div v-if="eventjob.data" class="w-3/4 mx-auto">
			<div class="p-4">
				<div class="flex mb-4">
					<img
						:src="eventjob.data.company_logo"
						class="w-16 h-16 rounded-lg object-contain mr-4"
						:alt="eventjob.data.company_name"
					/>
					<div>
						<div class="text-2xl font-semibold mb-4">
							{{ eventjob.data.eventjob_title }}
						</div>
						<div class="grid grid-cols-3 gap-8">
							<div class="grid grid-cols-1 gap-2">
								<div class="flex items-center space-x-2">
									<Building2 class="h-4 w-4 stroke-1.5" />
									<span>{{ eventjob.data.company_name }}</span>
								</div>
								<div class="flex items-center space-x-2">
									<MapPin class="h-4 w-4 stroke-1.5" />
									<span>{{ eventjob.data.location }}</span>
								</div>
							</div>
							<div class="grid grid-cols-1 gap-2">
								<div class="flex items-center space-x-2">
									<ClipboardType class="h-4 w-4 stroke-1.5" />
									<span>{{ eventjob.data.type }}</span>
								</div>
								<div class="flex items-center space-x-2">
									<CalendarDays class="h-4 w-4 stroke-1.5" />
									<span>{{
										dayjs(eventjob.data.creation).format('DD MMM YYYY')
									}}</span>
								</div>
							</div>
							<div class="grid grid-cols-1 h-fit">
								<div
									v-if="applicationCount.data"
									class="flex items-center space-x-2"
								>
									<SquareUserRound class="h-4 w-4 stroke-1.5" />
									<span
										>{{ applicationCount.data }}
										{{ __('applications received') }}</span
									>
								</div>
							</div>
						</div>
					</div>
				</div>
				<p
					v-html="eventjob.data.description"
					class="ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-gray-300 prose-th:border-gray-300 prose-td:relative prose-th:relative prose-th:bg-gray-100 prose-sm max-w-none !whitespace-normal mt-6"
				></p>
			</div>
			<EventJobApplicationModal
				v-model="showApplicationModal"
				v-model:application="eventjobApplication"
				:eventjob="eventjob.data.name"
			/>
		</div>
	</div>
</template>
<script setup>
import { Button, Breadcrumbs, createResource } from 'frappe-ui'
import { inject, ref, computed } from 'vue'
import { updateDocumentTitle } from '@/utils'
import EventJobApplicationModal from '@/components/Modals/EventJobApplicationModal.vue'
import {
	MapPin,
	SendHorizonal,
	Pencil,
	Building2,
	CalendarDays,
	ClipboardType,
	SquareUserRound,
} from 'lucide-vue-next'

const user = inject('$user')
const dayjs = inject('$dayjs')
const showApplicationModal = ref(false)

const props = defineProps({
	eventjob: {
		type: String,
		required: true,
	},
})

const eventjob = createResource({
	url: 'eventsconnect.eventsconnect.api.get_eventjob_details',
	params: {
		eventjob: props.eventjob,
	},
	cache: ['eventjob', props.eventjob],
	auto: true,
	onSuccess: (data) => {
		if (user.data?.name) {
			eventjobApplication.submit()
		}
		applicationCount.submit()
	},
})

const eventjobApplication = createResource({
	url: 'frappe.client.get_list',
	makeParams(values) {
		return {
			doctype: 'EventsConnect EventJob Application',
			filters: {
				eventjob: eventjob.data?.name,
				user: user.data?.name,
			},
		}
	},
})

const applicationCount = createResource({
	url: 'frappe.client.get_count',
	makeParams(values) {
		return {
			doctype: 'EventsConnect EventJob Application',
			filters: {
				eventjob: eventjob.data?.name,
			},
		}
	},
})

const openApplicationModal = () => {
	showApplicationModal.value = true
}

const redirectToLogin = (eventjob) => {
	window.location.href = `/login?redirect-to=/eventjob-openings/${eventjob}`
}

const pageMeta = computed(() => {
	return {
		title: eventjob.data?.eventjob_title,
		description: eventjob.data?.description,
	}
})

updateDocumentTitle(pageMeta)
</script>
