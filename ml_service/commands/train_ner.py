import argparse

from nlp.ner import NER


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "n_iter", nargs="?", default="10"
    )
    args = parser.parse_args()
    n_iter = int(args.n_iter)

    ner = NER()
    # train already evaluates model
    ner.train(n_iter)
    ner.save_model()
