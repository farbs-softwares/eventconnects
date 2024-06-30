<template>
	<div>
		<div class="flex items-center justify-between mb-4">
			<div class="text-xl font-semibold">
				{{ __('Courses') }}
			</div>
			<Button
				v-if="user.data?.is_moderator"
				variant="solid"
				@click="openCourseModal()"
			>
				<template #prefix>
					<Plus class="h-4 w-4" />
				</template>
				{{ __('Add Event') }}
			</Button>
		</div>
		<div v-if="events.data?.length">
			<ListView
				:columns="getCoursesColumns()"
				:rows="events.data"
				row-key="batch_event"
				:options="{
					showTooltip: false,
					getRowRoute: (row) => ({
						name: 'CourseDetail',
						params: { eventName: row.name },
					}),
				}"
			>
				<ListHeader
					class="mb-2 grid items-center space-x-4 rounded bg-gray-100 p-2"
				>
					<ListHeaderItem :item="item" v-for="item in getCoursesColumns()">
						<template #prefix="{ item }">
							<component
								v-if="item.icon"
								:is="item.icon"
								class="h-4 w-4 stroke-1.5 ml-4"
							/>
						</template>
					</ListHeaderItem>
				</ListHeader>
				<ListRows>
					<ListRow :row="row" v-for="row in events.data">
						<template #default="{ column, item }">
							<ListRowItem :item="row[column.key]" :align="column.align">
								<div>
									{{ row[column.key] }}
								</div>
							</ListRowItem>
						</template>
					</ListRow>
				</ListRows>
				<ListSelectBanner>
					<template #actions="{ unselectAll, selections }">
						<div class="flex gap-2">
							<Button
								variant="ghost"
								@click="removeCourses(selections, unselectAll)"
							>
								<Trash2 class="h-4 w-4 stroke-1.5" />
							</Button>
						</div>
					</template>
				</ListSelectBanner>
			</ListView>
		</div>
		<BatchCourseModal
			v-model="showCourseModal"
			:batch="batch"
			v-model:events="events"
		/>
	</div>
</template>
<script setup>
import { ref, inject } from 'vue'
import BatchCourseModal from '@/components/Modals/BatchCourseModal.vue'
import {
	createResource,
	Button,
	ListHeader,
	ListHeaderItem,
	ListSelectBanner,
	ListRow,
	ListRows,
	ListView,
	ListRowItem,
} from 'frappe-ui'
import { Plus, Trash2 } from 'lucide-vue-next'

const showCourseModal = ref(false)
const user = inject('$user')

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
})

const events = createResource({
	url: 'eventsconnect.eventsconnect.utils.get_batch_events',
	params: {
		batch: props.batch,
	},
	cache: ['batchCourses', props.batchName],
	auto: true,
})

const openCourseModal = () => {
	showCourseModal.value = true
}

const getCoursesColumns = () => {
	return [
		{
			label: 'Title',
			key: 'title',
			width: 2,
		},
		{
			label: 'Lessons',
			key: 'lesson_count',
			align: 'right',
		},
		{
			label: 'Enrollments',
			align: 'right',
			key: 'enrollment_count',
		},
	]
}

const removeCourse = createResource({
	url: 'frappe.client.delete',
	makeParams(values) {
		return {
			doctype: 'Batch Event',
			name: values.event,
		}
	},
})

const removeCourses = (selections, unselectAll) => {
	selections.forEach(async (event) => {
		removeCourse.submit({ event })
	})
	setTimeout(() => {
		events.reload()
		unselectAll()
	}, 1000)
}
</script>
