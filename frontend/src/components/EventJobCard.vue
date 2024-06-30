<template>
	<div class="flex rounded p-1 lg:px-2 lg:py-2.5 hover:bg-gray-100">
		<div class="flex w-3/5 md:w-2/5">
			<img
				:src="eventjob.company_logo"
				class="w-12 h-12 rounded-lg object-contain mr-4"
				:alt="eventjob.company_name"
			/>
			<div>
				<div class="font-medium mb-1">
					{{ eventjob.eventjob_title }}
				</div>
				<div class="text-gray-700">
					{{ eventjob.company_name }}
				</div>
			</div>
		</div>
		<div class="flex justify-end w-1/5 text-gray-700">
			{{ eventjob.location.replace(',', '').split(' ')[0] }}
		</div>
		<div
			class="flex justify-end w-1/5 text-gray-700 text-right hidden md:block"
		>
			{{ eventjob.type }}
		</div>
		<div class="flex justify-end w-1/5 text-sm text-gray-700 text-right">
			{{ dayjs(eventjob.creation).format('DD MMM YYYY') }}
		</div>
	</div>
	<!-- <div class="flex flex-col shadow rounded-md p-4 h-full">
		<div class="flex justify-between">
			<div>
				<div class="text-xl font-semibold mb-2">
					{{ eventjob.eventjob_title }}
				</div>
				<div>
					{{ __("posted by") }}
					<span class="font-medium">
						{{ eventjob.company_name }}
					</span>
				</div>
			</div>
			<img
				:src="eventjob.company_logo"
				class="w-12 h-12 rounded-lg object-contain"
			/>
		</div>
		<div class="flex justify-between mt-8">
			<div class="flex items-center">
				<Badge :label="eventjob.type" theme="green" size="lg" class="mr-4"/>
				<Badge :label="eventjob.location" theme="gray" size="lg">
					<template #prefix>
						<MapPin class="h-4 w-4 stroke-1.5" />
					</template>
				</Badge>
			</div>
			<div>
				<span class="font-medium">
					{{ dayjs(eventjob.creation).format('DD MMM YYYY') }}
				</span>
			</div>
		</div>
	</div> -->
</template>
<script setup>
import { MapPin } from 'lucide-vue-next'
import { Badge } from 'frappe-ui'
import { inject } from 'vue'

const dayjs = inject('$dayjs')
const props = defineProps({
	eventjob: {
		type: Object,
		default: null,
	},
})
</script>
