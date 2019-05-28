from __main__ import sio
from models import ProjectsModel, DomainsModel, IntentsModel, ResponseModel, StoryModel, EntityModel, RefreshDb
from export_project import ExportProject
from threading import Thread


EntityModel = EntityModel()
ProjectsModel = ProjectsModel()
DomainsModel = DomainsModel()
IntentsModel = IntentsModel()
ResponseModel = ResponseModel()
StoryModel = StoryModel()
ExportProject = ExportProject()
RefreshDb = RefreshDb()


@sio.on('connect')
async def connect(sid, environ):
    print('connect ', sid)
    print('Environment ', environ)


@sio.on('disconnect')
async def disconnect(sid):
    print('disconnect ', sid)

    # invoke cleanup of volumes
    result = await ExportProject.clean_up(sid)

    if result == 1:
        print("Clean up successful")
    else:
        print("-------------------- Error during cleanup ---------------------")


''' Refresh seed data. 

This method will wip off the mongo db instance of all user created data and reload it with seed data. 
This endpoint needs to be used with caution and ensure proper backup is taken before this is invoked '''


@sio.on('refresh_data', namespace='/refresh')
async def refresh_data(sid, data):
    print("##################################User {} Requested to refresh DB  ##########################".format(sid))

    result = await RefreshDb.refresh_db()
    await sio.emit('refresh', result)


'''Projects Endpoints 

These contains methods to get all projects , update delete and insert new project in the mongo db'''


@sio.on('getProjects', namespace='/project')
async def get_projects(sid, room_name):

    print("---------- Request from Session {} -------------- ".format(sid))

    result = await ProjectsModel.get_projects()
    await sio.emit('allProjects', result, namespace='/project', room=room_name)


@sio.on('createProject', namespace='/project')
async def create_projects(sid, record, room_name):

    print("---------- Request from Session {} -- with record {} ------------ ".format(sid, record))

    message = await ProjectsModel.create_projects(record)
    await sio.emit('projectResponse', message, namespace='/project', room=sid)

    if message['status'] == 'Success':
        result = await ProjectsModel.get_projects()
        await sio.emit('allProjects', result, namespace='/project', room=room_name)


@sio.on('deleteProject', namespace='/project')
async def delete_project(sid, object_id, room_name):

    print("---------- Request from Session {} --- with record {} ----------- ".format(sid, object_id))

    message = await ProjectsModel.delete_project(object_id)
    await sio.emit('projectResponse', message, namespace='/project', room=sid)

    result = await ProjectsModel.get_projects()
    await sio.emit('allProjects', result, namespace='/project', room=room_name)


@sio.on('updateProject', namespace='/project')
async def update_project(sid, update_query, room_name):

    print("---------- Request from Session {} - with record {} ------- ".format(sid, update_query))

    message = await ProjectsModel.update_project(update_query)
    await sio.emit('projectResponse', message, namespace='/project', room=sid)

    if message['status'] == 'Success':
        result = await ProjectsModel.get_projects()
        await sio.emit('allProjects', result, namespace='/project', room=room_name)


@sio.on('copyProject', namespace='/project')
async def copy_projects(sid, record, room_name):

    print("---------- Request from Session {} -- with record {} ------------ ".format(sid, record))

    message = await ProjectsModel.copy_project(record)
    await sio.emit('projectResponse', message, namespace='/project', room=sid)

    if message['status'] == 'Success':
        result = await ProjectsModel.get_projects()
        await sio.emit('allProjects', result, namespace='/project', room=room_name)

# Domains Endpoints


@sio.on('getDomains', namespace='/domain')
async def get_domains(sid, project_id, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ---------- ".format(sid, project_id, room_name))

    result = await DomainsModel.get_domains(project_id)
    await sio.emit('allDomains', result, namespace='/domain', room=room_name)


@sio.on('createDomain', namespace='/domain')
async def create_domain(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ---------- ".format(sid, data, room_name))

    message, domains_list = await DomainsModel.create_domain(data)
    await sio.emit('domainResponse', message, namespace='/domain', room=sid)

    if domains_list is not None:
        await sio.emit('allDomains', domains_list, namespace='/domain', room=room_name)


@sio.on('deleteDomain', namespace='/domain')
async def delete_domain(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ---------- ".format(sid, data, room_name))

    message, domains_list = await DomainsModel.delete_domain(data)

    await sio.emit('domainResponse', message, namespace='/domain', room=sid)
    await sio.emit('allDomains', domains_list, namespace='/domain', room=room_name)


@sio.on('updateDomain', namespace='/domain')
async def update_domains(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, domains_list = await DomainsModel.update_domain(data)
    print("Message value {}".format(message))
    await sio.emit('domainResponse', message, room=sid, namespace='/domain')

    if domains_list is not None:
        await sio.emit('allDomains', domains_list, namespace='/domain', room=room_name)


@sio.on('importDomain', namespace='/domain')
async def import_domains(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    # TODO
    await sio.emit('domainResponse', "Message", room=sid, namespace='/domain')


@sio.on('updateDomainStatus', namespace='/domain')
async def update_domains_status(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    # TODO
    await sio.emit('domainResponse', "Message", room=sid, namespace='/domain')


# intents Endpoint


@sio.on('getIntents', namespace='/dashboard')
async def get_intents(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    intents_list = await IntentsModel.get_intents(data)
    await sio.emit('allIntents', intents_list, namespace='/dashboard', room=room_name)


@sio.on('createIntent', namespace='/dashboard')
async def create_intent(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intents_list = await IntentsModel.create_intent(data)
    await sio.emit('intentResponse', message, namespace='/dashboard', room=sid)

    if intents_list is not None:
        await sio.emit('allIntents', intents_list, namespace='/dashboard', room=room_name)


@sio.on('deleteIntent', namespace='/dashboard')
async def delete_intent(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intents_list = await IntentsModel.delete_intent(data)

    await sio.emit('intentResponse', message, namespace='/dashboard', room=sid)
    await sio.emit('allIntents', intents_list, namespace='/dashboard', room=room_name)


@sio.on('updateIntent', namespace='/dashboard')
async def update_intent(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intents_list = await IntentsModel.update_intent(data)
    await sio.emit('intentResponse', message, namespace='/dashboard', room=sid)

    if intents_list is not None:
        await sio.emit('allIntents', intents_list, namespace='/dashboard', room=room_name)


@sio.on('getIntentDetails', namespace='/intent')
async def get_intent_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    intent_detail = await IntentsModel.get_intent_details(data)
    await sio.emit('intentDetail', intent_detail, namespace='/intent', room=room_name)


@sio.on('insertIntentDetails', namespace='/intent')
async def insert_intent_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intent_detail = await IntentsModel.insert_intent_detail(data)
    await sio.emit('respIntentDetail', message, namespace='/intent', room=sid)
    await sio.emit('intentDetail', intent_detail, namespace='/intent', room=room_name)


@sio.on('updateIntentDetails', namespace='/intent')
async def update_intent_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intent_detail = await IntentsModel.update_intent_detail(data)
    await sio.emit('respIntentDetail', message, namespace='/intent', room=sid)
    await sio.emit('intentDetail', intent_detail, namespace='/intent', room=room_name)


@sio.on('deleteIntentDetails', namespace='/intent')
async def insert_intent_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intent_detail = await IntentsModel.delete_intent_detail(data)
    await sio.emit('respIntentDetail', message, namespace='/intent', room=sid)
    await sio.emit('intentDetail', intent_detail, namespace='/intent', room=room_name)


# responses Endpoints


@sio.on('getResponses', namespace='/dashboard')
async def get_responses(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    responses_list = await ResponseModel.get_responses(data)
    await sio.emit('allResponses', responses_list, namespace='/dashboard', room=room_name)


@sio.on('createResponse', namespace='/dashboard')
async def create_response(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, responses_list = await ResponseModel.create_response(data)

    await sio.emit('respResponse', message, namespace='/dashboard', room=sid)

    if responses_list is not None:
        await sio.emit('allResponses', responses_list, namespace='/dashboard', room=room_name)


@sio.on('deleteResponse', namespace='/dashboard')
async def delete_response(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, responses_list = await ResponseModel.delete_response(data)

    await sio.emit('respResponse', message, namespace='/dashboard', room=sid)
    await sio.emit('allResponses', responses_list, namespace='/dashboard', room=room_name)


@sio.on('updateResponse', namespace='/dashboard')
async def update_response(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, responses_list = await ResponseModel.update_response(data)
    await sio.emit('respResponse', message, namespace='/dashboard', room=sid)

    if responses_list is not None:
        await sio.emit('allResponses', responses_list, namespace='/dashboard', room=room_name)


@sio.on('getResponseDetails', namespace='/response')
async def get_response_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room  ----------  ".format(sid, data))

    intent_detail = await ResponseModel.get_response_details(data)
    await sio.emit('responseDetail', intent_detail, namespace='/response', room=room_name)


@sio.on('insertResponseDetails', namespace='/response')
async def insert_response_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intent_detail = await ResponseModel.insert_response_detail(data)
    await sio.emit('respResponseDetail', message, namespace='/response', room=sid)
    await sio.emit('responseDetail', intent_detail, namespace='/response', room=room_name)


@sio.on('updateResponseDetails', namespace='/response')
async def update_response_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intent_detail = await ResponseModel.update_response_detail(data)
    await sio.emit('respResponseDetail', message, namespace='/response', room=sid)
    await sio.emit('responseDetail', intent_detail, namespace='/response', room=room_name)


@sio.on('deleteResponseDetails', namespace='/response')
async def insert_response_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, intent_detail = await ResponseModel.delete_response_detail(data)
    await sio.emit('respResponseDetail', message, namespace='/response', room=sid)
    await sio.emit('responseDetail', intent_detail, namespace='/response', room=room_name)


# Endpoints for Stories


@sio.on('getStories', namespace='/dashboard')
async def get_stories(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    stories_list = await StoryModel.get_stories(data)
    await sio.emit('allStories', stories_list, namespace='/dashboard', room=room_name)


@sio.on('createStory', namespace='/dashboard')
async def create_story(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, stories_list = await StoryModel.create_story(data)
    await sio.emit('storyResponse', message, namespace='/dashboard', room=sid)

    if stories_list is not None:
        await sio.emit('allStories', stories_list, namespace='/dashboard', room=room_name)


@sio.on('deleteStory', namespace='/dashboard')
async def delete_story(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, stories_list = await StoryModel.delete_story(data)

    await sio.emit('storyResponse', message, namespace='/dashboard', room=sid)
    await sio.emit('allStories', stories_list, namespace='/dashboard', room=room_name)


@sio.on('updateStory', namespace='/dashboard')
async def update_story(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, stories_list = await StoryModel.update_story(data)

    await sio.emit('storyResponse', message, namespace='/dashboard', room=sid)

    if stories_list is not None:
        await sio.emit('allStories', stories_list, namespace='/dashboard', room=room_name)


@sio.on('getStoryDetails', namespace='/story')
async def get_story_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room  ----------  ".format(sid, data))

    story_detail, intents_list, response_list = await StoryModel.get_story_details(data)
    await sio.emit('storyDetail', story_detail, namespace='/story', room=room_name)
    await sio.emit('allIntents', intents_list, namespace='/story', room=room_name)
    await sio.emit('allResponses', response_list, namespace='/story', room=room_name)


@sio.on('insertStoryDetails', namespace='/story')
async def insert_story_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room  ----------  ".format(sid, data))

    message, story_detail, intents_list, response_list = await StoryModel.insert_story_details(data)
    await sio.emit('respStoryDetail', message, namespace='/story', room=sid)
    await sio.emit('storyDetail', story_detail, namespace='/story', room=room_name)
    await sio.emit('allIntents', intents_list, namespace='/story', room=room_name)
    await sio.emit('allResponses', response_list, namespace='/story', room=room_name)


@sio.on('deleteStoryDetails', namespace='/story')
async def delete_story_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, story_detail, intents_list, response_list = await StoryModel.delete_story_detail(data)
    await sio.emit('respStoryDetail', message, namespace='/story', room=sid)
    await sio.emit('storyDetail', story_detail, namespace='/story', room=room_name)
    await sio.emit('allIntents', intents_list, namespace='/story', room=room_name)
    await sio.emit('allResponses', response_list, namespace='/story', room=room_name)


@sio.on('updateStoryDetails', namespace='/story')
async def update_story_details(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, story_detail, intents_list, response_list = await StoryModel.update_story_detail(data)
    await sio.emit('respStoryDetail', message, namespace='/story', room=sid)
    await sio.emit('storyDetail', story_detail, namespace='/story', room=room_name)
    await sio.emit('allIntents', intents_list, namespace='/story', room=room_name)
    await sio.emit('allResponses', response_list, namespace='/story', room=room_name)

# Entities Endpoints


@sio.on('getEntities', namespace='/nav')
async def get_entities(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    entities_list = await EntityModel.get_entities(data)
    await sio.emit('allEntities', entities_list, namespace='/nav', room=room_name)


@sio.on('createEntity', namespace='/nav')
async def create_entity(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    message, entities_list = await EntityModel.create_entity(data)
    await sio.emit('entitiesResponse', message, namespace='/nav', room=room_name)

    if entities_list is not None:
        await sio.emit('allEntities', entities_list, namespace='/nav', room=room_name)


@sio.on('deleteEntity', namespace='/nav')
async def delete_entity(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))

    message, entities_list = await EntityModel.delete_entity(data)

    await sio.emit('entitiesResponse', message, namespace='/nav', room=sid)
    await sio.emit('allEntities', entities_list, namespace='/nav', room=room_name)


@sio.on('updateEntity', namespace='/nav')
async def update_entity(sid, data, room_name):

    print("---------- Request from Session {} -- with record {} -- and room {} ----------  ".format(sid, data, room_name))
    message, entities_list = await EntityModel.update_entity(data)
    await sio.emit('entitiesResponse', message, namespace='/nav', room=room_name)

    if entities_list is not None:
        await sio.emit('allEntities', entities_list, namespace='/nav', room=room_name)


@sio.on('exportProject', namespace='/train')
async def export_project(sid, data):
    print("---------- Request from Session {} -- with record {} -- and room  ----------  ".format(sid, data))

    result = await ExportProject.main(sid, data)
    print("Result of Export project {}".format(result))


@sio.on('tryNow', namespace='/trynow')
async def try_now(sid, data):
    print("----------- Inside Try now --from SID {}--------------".format(sid))
    result = await ExportProject.main(sid, data)
    print(result)
    from try_now import TryNow
    room_name = "TEST"
    trynow = TryNow()
    worker = Thread(target=trynow.chat_now, args=(sid, room_name, data,))
    worker.start()
