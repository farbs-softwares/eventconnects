<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Schedule Evaluation'),
			size: 'xl',
			actions: [
				{
					label: __('Submit'),
					variant: 'solid',
					onClick: (close) => submitEvaluation(close),
				},
			],
		}"
	>
		<template #body-content>
			<div class="flex flex-col gap-4">
				<div>
					<div class="mb-1.5 text-sm text-gray-600">
						{{ __('Event') }}
					</div>
					<Select v-model="evaluation.event" :options="getCourses()" />
				</div>
				<div>
					<div class="mb-1.5 text-sm text-gray-600">
						{{ __('Date') }}
					</div>
					<FormControl type="date" v-model="evaluation.date" />
				</div>
				<div v-if="slots.data?.length">
					<div class="mb-1.5 text-sm text-gray-600">
						{{ __('Select a slot') }}
					</div>
					<div class="grid grid-cols-2 gap-2">
						<div v-for="slot in slots.data">
							<div
								class="text-base text-center border rounded-md bg-gray-200 p-2 cursor-pointer"
								@click="saveSlot(slot)"
								:class="{
									'border-gray-900': evaluation.start_time == slot.start_time,
								}"
							>
								{{ formatTime(slot.start_time) }} -
								{{ formatTime(slot.end_time) }}
							</div>
						</div>
					</div>
				</div>
				<div
					v-else-if="evaluation.event && evaluation.date"
					class="text-sm italic text-red-600"
				>
					{{ __('No slots available for this date.') }}
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import { Dialog, createResource, Select, FormControl } from 'frappe-ui'
import { defineModel, reactive, watch, inject } from 'vue'
import { createToast, formatTime } from '@/utils/'

const user = inject('$user')
const dayjs = inject('$dayjs')
const show = defineModel()
const evaluations = defineModel('reloadEvals')

const props = defineProps({
	events: {
		type: Array,
		default: [],
	},
	batch: {
		type: String,
		default: null,
	},
	endDate: {
		type: String,
		default: null,
	},
})

let evaluation = reactive({
	event: '',
	date: '',
	start_time: '',
	end_time: '',
	day: '',
	batch: props.batch,
	member: user.data.name,
})

const createEvaluation = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'EventsConnect Certificate Request',
				batch_name: values.batch,
				...values,
			},
		}
	},
})

function submitEvaluation(close) {
	createEvaluation.submit(evaluation, {
		validate() {
			if (!evaluation.event) {
				return 'Please select a event.'
			}
			if (!evaluation.date) {
				return 'Please select a date.'
			}
			if (!evaluation.start_time) {
				return 'Please select a slot.'
			}
			if (dayjs(evaluation.date).isBefore(dayjs(), 'day')) {
				return 'Please select a future date.'
			}
			if (dayjs(evaluation.date).isAfter(dayjs(props.endDate), 'day')) {
				return `Please select a date before the end date ${dayjs(
					props.endDate
				).format('DD MMMM YYYY')}.`
			}
		},
		onSuccess() {
			evaluations.value.reload()
			close()
		},
		onError(err) {
			createToast({
				title: 'Error',
				text: err.messages?.[0] || err,
				icon: 'x',
				iconClasses: 'bg-red-600 text-white rounded-md p-px',
				position: 'top-center',
				timeout: 10,
			})
		},
	})
}

const getCourses = () => {
	let events = []
	for (const event of props.events) {
		events.push({
			label: event.title,
			value: event.event,
		})
	}
	return events
}

const slots = createResource({
	url: 'eventsconnect.eventsconnect.doctype.event_evaluator.event_evaluator.get_schedule',
	makeParams(values) {
		return {
			event: values.event,
			date: values.date,
			batch: props.batch,
		}
	},
})

watch(
	() => evaluation.date,
	(date) => {
		evaluation.start_time = ''
		if (date && evaluation.event) {
			slots.submit(evaluation)
		}
	}
)

watch(
	() => evaluation.event,
	(event) => {
		evaluation.date = ''
		evaluation.start_time = ''
		slots.reset()
	}
)

const saveSlot = (slot) => {
	evaluation.start_time = slot.start_time
	evaluation.end_time = slot.end_time
	evaluation.day = slot.day
}
</script>
