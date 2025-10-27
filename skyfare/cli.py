import argparse
from .pipeline import TrainPipeline, PredictPipeline


def main():
    parser = argparse.ArgumentParser(description="SkyFareAI CLI")
    sub = parser.add_subparsers(dest="cmd")

    train = sub.add_parser("train")
    train.add_argument("--config", default="config/default_config.yaml")
    train.add_argument("--train_csv", required=True)
    train.add_argument("--out", default="artifacts/skyfare_model.joblib")

    pred = sub.add_parser("predict")
    pred.add_argument("--artifact", required=True)
    pred.add_argument("--input_csv", required=True)
    pred.add_argument("--output_csv", default=None)

    args = parser.parse_args()

    if args.cmd == "train":
        metrics = TrainPipeline(args.config).run(args.train_csv, args.out)
        print(metrics)
    elif args.cmd == "predict":
        out_df = PredictPipeline(args.artifact).run(args.input_csv)
        if args.output_csv:
            out_df.to_csv(args.output_csv, index=False)
        print(out_df.head())


if __name__ == "__main__":
    main()
