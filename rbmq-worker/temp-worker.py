# sample worker script
# defined entrypoint "work" is called by setup.py
import regex

# import chipper

def work(context, inputs, parameters, responder):
    print('work called')
    print(regex)
    model = {'inputs': inputs}
    responder(context, model)
    # new_task = parameters.subtask_description
    # new_task['specificdetails'] = yadayada
    # chipper.work_enqueue(new_task)
    return {'status':'ok'}