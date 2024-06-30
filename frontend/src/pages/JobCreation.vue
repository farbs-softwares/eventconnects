<template>
	<div class="">
		<header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs :items="breadcrumbs" />
			<Button variant="solid" @click="saveEventJob()">
				{{ __('Save') }}
			</Button>
		</header>
		<div class="py-5">
			<div class="container border-b mb-4 pb-4">
				<div class="text-lg font-semibold mb-4">
					{{ __('EventJob Details') }}
				</div>
				<div class="grid grid-cols-2 gap-4">
					<div>
						<FormControl
							v-model="eventjob.eventjob_title"
							:label="__('Title')"
							class="mb-4"
						/>
						<FormControl v-model="eventjob.location" :label="__('Location')" />
					</div>
					<div>
						<FormControl
							v-model="eventjob.type"
							:label="__('Type')"
							type="select"
							:options="eventjobTypes"
							class="mb-4"
						/>
						<FormControl
							v-model="eventjob.status"
							:label="__('Status')"
							type="select"
							:options="eventjobStatuses"
						/>
					</div>
				</div>
				<div class="mt-4">
					<label class="block text-gray-600 text-xs mb-1">
						{{ __('Description') }}
					</label>
					<TextEditor
						:content="eventjob.description"
						@change="(val) => (eventjob.description = val)"
						:editable="true"
						:fixedMenu="true"
						editorClass="prose-sm max-w-none border-b border-x bg-gray-100 rounded-b-md py-1 px-2 min-h-[7rem] mb-4"
					/>
				</div>
			</div>
			<div class="container mb-4 pb-4">
				<div class="text-lg font-semibold mb-4">
					{{ __('Company Details') }}
				</div>
				<div class="grid grid-cols-2 gap-4">
					<div>
						<FormControl
							v-model="eventjob.company_name"
							:label="__('Company Name')"
							class="mb-4"
						/>
						<FormControl
							v-model="eventjob.company_website"
							:label="__('Company Website')"
						/>
					</div>
					<div>
						<FormControl
							v-model="eventjob.company_email_address"
							:label="__('Company Email Address')"
							class="mb-4"
						/>
						<label class="block text-gray-600 text-xs mb-1 mt-4">
							{{ __('Company Logo') }}
						</label>
						<FileUploader
							v-if="!eventjob.image"
							:fileTypes="['image/*']"
							:validateFile="validateFile"
							@success="(file) => saveImage(file)"
						>
							<template
								v-slot="{ file, progress, uploading, openFileSelector }"
							>
								<div class="mb-4">
									<Button @click="openFileSelector" :loading="uploading">
										{{
											uploading ? `Uploading ${progress}%` : 'Upload an image'
										}}
									</Button>
								</div>
							</template>
						</FileUploader>
						<div v-else class="">
							<div class="flex items-center">
								<div class="border rounded-md p-2 mr-2">
									<FileText class="h-5 w-5 stroke-1.5 text-gray-700" />
								</div>
								<div class="flex flex-col">
									<span>
										{{ eventjob.image.file_name }}
									</span>
									<span class="text-sm text-gray-500 mt-1">
										{{ getFileSize(eventjob.image.file_size) }}
									</span>
								</div>
								<X
									@click="removeImage()"
									class="bg-gray-200 rounded-md cursor-pointer stroke-1.5 w-5 h-5 p-1 ml-4"
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	Breadcrumbs,
	FormControl,
	createResource,
	Button,
	TextEditor,
	FileUploader,
} from 'frappe-ui'
import { computed, onMounted, reactive, inject } from 'vue'
import { FileText, X } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { getFileSize, showToast } from '../utils'

const user = inject('$user')
const router = useRouter()

const props = defineProps({
	eventjobName: {
		type: String,
		default: 'new',
	},
})

const newEventJob = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'EventJob Opportunity',
				company_logo: eventjob.image.file_url,
				...eventjob,
			},
		}
	},
})

const updateEventJob = createResource({
	url: 'frappe.client.set_value',
	makeParams(values) {
		return {
			doctype: 'EventJob Opportunity',
			name: props.eventjobName,
			fieldname: {
				company_logo: eventjob.image.file_url,
				...eventjob,
			},
		}
	},
})

const eventjobDetail = createResource({
	url: 'frappe.client.get',
	makeParams(values) {
		return {
			doctype: 'EventJob Opportunity',
			name: props.eventjobName,
		}
	},
	onSuccess(data) {
		Object.keys(data).forEach((key) => {
			if (Object.hasOwn(eventjob, key)) eventjob[key] = data[key]
		})
		if (data.company_logo) imageResource.reload({ image: data.company_logo })
	},
})

const imageResource = createResource({
	url: 'eventsconnect.eventsconnect.api.get_file_info',
	makeParams(values) {
		return {
			file_url: values.image,
		}
	},
	auto: false,
	onSuccess(data) {
		eventjob.image = data
	},
})

const eventjob = reactive({
	eventjob_title: '',
	location: '',
	type: 'Full Time',
	status: 'Open',
	company_name: '',
	company_website: '',
	image: null,
	description: '',
	company_email_address: '',
})

onMounted(() => {
	if (!user.data) window.location.href = '/login'

	if (props.eventjobName != 'new') eventjobDetail.reload()
})

const saveEventJob = () => {
	if (eventjobDetail.data) {
		editEventJobDetails()
	} else {
		createNewEventJob()
	}
}

const createNewEventJob = () => {
	newEventJob.submit(
		{},
		{
			onSuccess(data) {
				router.push({
					name: 'EventJobDetail',
					params: {
						eventjob: data.name,
					},
				})
			},
			onError(err) {
				showToast('Error', err.messages?.[0] || err, 'x')
			},
		}
	)
}

const editEventJobDetails = () => {
	updateEventJob.submit(
		{},
		{
			onSuccess(data) {
				router.push({
					name: 'EventJobDetail',
					params: {
						eventjob: data.name,
					},
				})
			},
			onError(err) {
				showToast('Error', err.messages?.[0] || err, 'x')
			},
		}
	)
}

const saveImage = (file) => {
	eventjob.image = file
}

const removeImage = () => {
	eventjob.image = null
}

const validateFile = (file) => {
	let extension = file.name.split('.').pop().toLowerCase()
	if (!['jpg', 'jpeg', 'png'].includes(extension)) {
		return 'Only image file is allowed.'
	}
}

const eventjobTypes = computed(() => {
	return [
		{ label: 'Full Time', value: 'Full Time' },
		{ label: 'Part Time', value: 'Part Time' },
		{ label: 'Contract', value: 'Contract' },
		{ label: 'Freelance', value: 'Freelance' },
	]
})

const eventjobStatuses = computed(() => {
	return [
		{ label: 'Open', value: 'Open' },
		{ label: 'Closed', value: 'Closed' },
	]
})

const breadcrumbs = computed(() => {
	let crumbs = [
		{
			label: 'EventJobs',
			route: { name: 'EventJobs' },
		},
		{
			label: props.eventjobName == 'new' ? 'New EventJob' : 'Edit EventJob',
			route: { name: 'EventJobCreation' },
		},
	]
	return crumbs
})
</script>
