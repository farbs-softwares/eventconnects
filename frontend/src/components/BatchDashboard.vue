<template>
	<div>
		<UpcomingEvaluations
			:batch="batch.data.name"
			:endDate="batch.data.evaluation_end_date"
			:events="batch.data.events"
			:isStudent="isStudent"
		/>
		<Assessments :batch="batch.data.name" />
	</div>
</template>
<script setup>
import UpcomingEvaluations from '@/components/UpcomingEvaluations.vue'
import Assessments from '@/components/Assessments.vue'

const props = defineProps({
	batch: {
		type: Object,
		default: null,
	},
	isStudent: {
		type: Boolean,
		default: false,
	},
})
</script>
