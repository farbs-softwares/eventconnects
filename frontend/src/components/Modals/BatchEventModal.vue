<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Add a event'),
			size: 'sm',
			actions: [
				{
					label: __('Submit'),
					variant: 'solid',
					onClick: (close) => addCourse(close),
				},
			],
		}"
	>
		<template #body-content>
			<Link doctype="EventsConnect Event" v-model="event" :label="__('Event')" />
			<Link
				doctype="Event Evaluator"
				v-model="evaluator"
				:label="__('Evaluator')"
				class="mt-4"
			/>
		</template>
	</Dialog>
</template>
<script setup>
import { Dialog, createResource } from 'frappe-ui'
import { ref, defineModel } from 'vue'
import Link from '@/components/Controls/Link.vue'
import { showToast } from '@/utils'

const show = defineModel()
const event = ref(null)
const evaluator = ref(null)
const events = defineModel('events')

const props = defineProps({
	batch: {
		type: String,
		default: null,
	},
})

const createBatchCourse = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'Batch Event',
				parent: props.batch,
				parenttype: 'EventsConnect Batch',
				parentfield: 'events',
				event: event.value,
				evaluator: evaluator.value,
			},
		}
	},
})

const addCourse = (close) => {
	createBatchCourse.submit(
		{},
		{
			onSuccess() {
				events.value.reload()
				close()
				event.value = null
				evaluator.value = null
			},
			onError(err) {
				showToast('Error', err.message[0] || err, 'x')
			},
		}
	)
}
</script>
