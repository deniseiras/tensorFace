import time
from src.controller.face_recognition.face_tester.label_image_func import *
from src.debug.debugutils import DebugUtils

debug = DebugUtils.get_instance()


def test(exp, file_name):
    # debug.msg("\n ===> TESTING file {} ".format(file_name))
    millis_init = time.time()

    # default values
    if exp["architecture"] == 'inception_v3':
        input_layer = "Mul"
        exp["input_height"] = 299 if exp["input_height"] is None else exp["input_height"]
        exp["input_width"] = 299 if exp["input_width"] is None else exp["input_width"]
        exp["input_mean"] = 0 if exp["input_mean"] is None else exp["input_mean"]
        exp["input_std"] = 255 if exp["input_std"] is None else exp["input_std"]
    else:
        input_layer = "input"
        exp["input_height"] = 224 if exp["input_height"] is None else exp["input_height"]
        exp["input_width"] = 224 if exp["input_width"] is None else exp["input_width"]
        exp["input_mean"] = 128 if exp["input_mean"] is None else exp["input_mean"]
        exp["input_std"] = 128 if exp["input_std"] is None else exp["input_std"]

    output_layer = "final_result"
    model_file = exp["model_file"]
    label_file = exp["label_file"]

    # TODO - do once
    graph = load_graph(model_file)

    t = read_tensor_from_image_file(file_name,
                                    input_height=exp["input_height"],
                                    input_width=exp["input_width"],
                                    input_mean=exp["input_mean"],
                                    input_std=exp["input_std"])

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name);
    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
    results = np.squeeze(results)
    top_k = results.argsort()[-10:][::-1]
    labels = load_labels(label_file)
    labels_results = {}
    for i in top_k:
        labels_results[labels[i]] = results[i]
        # debug.msg(labels[i], ' {0:.4f}%'.format(results[i]*100))
    millis_end = time.time()
    time_exec = millis_end - millis_init
    return labels_results, time_exec
